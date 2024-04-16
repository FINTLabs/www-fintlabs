# Error handling

## How to deal with errors

Since `UPDATE_` events involves multiple components and is based on events,
errors are bound to happen. 

## Update conflicts

Sometimes the update attempted is in conflict with other data in the back-end
system.  This could for instance be:

 - Attempts to create data with identifiers that refer to existing information.
 - Modifications that create illegal state when combined with existing information.

 In both cases, the adapter must reject the update with `CONFLICT` response status.  Furthermore, the response must contain the payload that the original
 update conflicts with.

 This enables the client to update its information and possibly modify the
 update before another attempt is made.

## Lost events

The update events could be lost at multiple stages of the flow.  To better
illustrate where this happens, let's first describe the successful scenario.

### Successful case

The following sequence diagram illustrates the successful case, where 
information is updated, and the client successfully recieves confirmation
of the update.

<img src="/images/normal.svg" alt="Successful case sequence diagram" class="img-responsive" style="background:#fff" />

### Event is lost before it reaches adapter

This is the simplest failure scenaro to handle.  Nobody gets informed of the
update, and the update can safely be retried after the original update
has expired.

<img src="/images/timeout.svg" alt="Timeout case sequence diagram" class="img-responsive" style="background:#fff" />

### Event is confirmed by adapter, but not updated in back-end system

This scenario is very similar to the one above - the only difference is 
the time it takes for the event to expire.

<img src="/images/noresponse.svg" alt="No response case sequence diagram" class="img-responsive" style="background:#fff" />

### Event is confirmed and updated in back-end system, but client is not notified

This is the most difficult scenario.  Since the back-end system has been 
updated, the event cannot safely be retried, although the client does not
know.  There are basically two ways to resolve this issue.

Which of these is better depends on the back-end system's ability to record
and roll back pending modifications.


#### Roll back the modification so it can safely be retried.

<img src="/images/orphaned.svg" alt="Orphaned case sequence diagram" class="img-responsive" style="background:#fff"/>

For this case to be possible, the connection between the
adapter and the back-end system must support transaction
rollback, or similar compensating operations.

#### Use conflict detection to reject a retry with `CONFLICT` status.

<img src="/images/duplicate.svg" alt="Duplicate case sequence diagram" class="img-responsive" style="background:#fff" />

In this latter case, client support is required for the state
of the update to be synchronized correctly between client and
back-end system.  For this to work, it is essential that the
adapter correctly responds to the `CONFLICT` with a response
payload indicating the current state of the information in the
back-end system, and that the client correctly handles the
`409` status and updates its pending transaction with this
information.
