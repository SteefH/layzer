ng = @angular

ng.module('layzer').controller 'FeedItemsCtrl', [
  '$scope', 'feedItems', '$routeParams', 'feeditemsservice'
  ($scope ,  feeditems ,  $routeParams ,  feeditemsservice) ->

    ng.extend $scope,
      items: feeditems.items
      hasNext: feeditems.hasNext
      _shownItem: null

      isShown: (item) ->
        item.id == $scope._shownItem

      showItem: (item) ->
        if $scope.isShown item
          $scope._shownItem = null
        else
          item.bodyIfShown = item.body
          $scope._shownItem = item.id
          $scope.markRead item

      loadMore: ->
        return unless $scope.hasNext

        feeditemsservice.nextForFeed($routeParams.feed).then (items) ->
          $scope.items = items.items
          $scope.hasNext = items.hasNext

      markRead: (item) ->
        feeditemsservice.markRead item

      itemClass: (item) ->
        classes = []
        classes.push('read') if item.marked_read
        classes.join ' '

]
