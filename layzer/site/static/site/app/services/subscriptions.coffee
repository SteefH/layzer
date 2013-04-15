ng = @angular
ng.module('layzer').factory 'subscriptionsservice', [
    '$resource', '$q'
    ($resource,   $q) ->
        Subscription = $resource '/api/v1/subscription/:id', id: '@id',
            query:
                method: 'GET'
                isArray: true
                transformResponse: (data) ->
                    data = ng.fromJson data
                    data.objects
            update:
                method: 'PUT'

        withPromise = (fn) ->
            (args...) ->
                deferred = $q.defer()
                args.push(
                    (a...) -> deferred.resolve(a...)
                    (a...) -> deferred.reject(a...)
                )
                fn.apply @, args
                deferred.promise

        callWithPromise = (fn, rest...) ->
            withPromise(fn) rest...


        getAll: (args...) -> Subscription.query(args...)
        add: (url) ->
            sub = new Subscription site_url: url
            callWithPromise (a...) -> sub.$save a...
        edit: (sub) -> callWithPromise (a...) -> sub.$update a...
        remove: (sub) -> callWithPromise (a...) -> sub.$delete a...
]


