# Updating information using FINT APIs

## Updating information using FINT

Updates use HTTP operations to create, modify and delete information.  It builds upon the "everything
is a resource" principle, so when updating information the resource URI is central.

### Asynchronous operations

Since the updates must propagate via the FINT component and an adapter before being processed by the
back end system, updates might take some time to complete.  For this, FINT APIs use asynchronous
operations as described in http://restcookbook.com/Resources/asynchroneous-operations/.

The process is as follows:

1. The client initiates an update operation.
1. The FINT API validates the syntax of the operation and responds with status code `202` and a `Location` 
   header referring to a `/status/<uuid>` resource
1. The client fetches the *Status* resource.
   - If the operation is still pending, the FINT API keeps responding with status code `202`.
1. If the operation has completed, the FINT API responds with the final status of the update:
   - If successful, status `201` with a `Location` referring to the resource that has been
     created or updated, and a payload with the updated resource.
   - _Note:_ If the operation is a deletion, the status code is `204` instead.
   - If rejected by the back-end system, status `400` with a response body indicating the error.
   - If the update is in conflict with other updates or data in the back-end system, the status
     is `409` and the response body contains the original information the update conflicts with.
   - If there was a temporary failure processing the request, status `500` with the
     error message.
      In this case the client can re-try the request.

The *Status* resource is valid for 30 minutes after initiating the original request.

### Creating new objects

`POST /domain/package/class`, i.e. 
`POST /administrasjon/personal/fravar`

The body must be a complete resource to be created, including `_links` to other resources it refers to.

Internal identifiers controlled by the back-end system can be omitted.

### Modifying existing objects

`PUT /domain/package/class/field/value`, i.e. `PUT /administrasjon/personal/personalressurs/ansattnummer/123456`

The resource to be modified is identified by the identifiable field and value.
Any field of type `Identifikator` can be used to identify the resource.

The body must be the complete resource after modification.
Attributes that can be modified are indicated in the information model.

### Deleting objects

`DELETE /domain/package/class/field/value`, i.e. `DELETE /administrasjon/personal/fravar/systemid/abcdef1234`

Not all information classes support deletion.
If deletion is not supported, the operation is rejected with status `400`.
