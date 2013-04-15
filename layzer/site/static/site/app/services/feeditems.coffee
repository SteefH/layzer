ng = @angular

ng.module('layzer').factory 'feeditemsservice', [
  '$http', '$q'
  ($http,   $q) ->
    forFeed = {}

    getForFeed: (feedUrl) ->
      $http.get('/api/v1/feeditem?feed=' + encodeURIComponent(feedUrl))
        .then (result) ->
          forFeed[feedUrl] =
            next: result.data.meta.next
            objects: result.data.objects
          items: result.data.objects
          hasNext: !!result.data.meta.next

    nextForFeed: (feedUrl) ->
      forThisFeed = forFeed[feedUrl]
      return this.getForFeed feedUrl unless forThisFeed
      if !forThisFeed.promise
        callback = (result) ->
          ng.extend forThisFeed,
              next: result.data.meta.next
              objects: forThisFeed.objects.concat result.data.objects
              promise: null

          items: forThisFeed.objects
          hasNext: !!result.data.meta.next
        errback = (e) ->
          forThisFeed.promise = null
          throw e

        forThisFeed.promise = $http.get(forThisFeed.next).then callback, errback
      forThisFeed.promise

    markRead: (item) ->
      return if item.marked_read
      data = marked_read: true
      $http.put(item.resource_uri, data).then -> item.marked_read = true
]
