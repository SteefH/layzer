
ng = @angular

ng.module('layzer').controller 'SubscriptionsCtrl', [
  '$scope', 'subscriptionsservice'
  ($scope,   subscriptions) ->
    $scope.subscriptions = subscriptions.getAll()
    $scope.rename =
      active: false
      start: (subscription) ->
        @subscription = subscription
        @active = true
        @newName = subscription.name

      submit: ->
        @subscription.name = @newName
        subscriptions.edit @subscription

      end: -> @active = false

    $scope.remove =
      active: false
      start: (subscription) ->
        @subscription = subscription
        @active = true

      submit: ->
        subscriptions.remove(this.subscription).then (removed) ->
          $scope.subscriptions = (sub for sub in $scope.subscriptions when sub.id != removed.id)
        @active = false

      end: -> @active = false

    $scope.subscribe =
      start: ->
        @url = ''
        @active = true

      end: -> @active = false

      submit: ->
        subscriptions.add(@url).then(
          (sub) ->
            $scope.subscriptions.push sub
          (response) ->
            return unless response.status == 409
            $scope.alert.start 'Je bent al geabonneerd op deze site'
        )
    $scope.alert =
      start: (message) ->
        @message = message
        @active = true
      end: ->
        @active = false

    $scope.subscriptionLink = (s) ->
      '#/feed/' + encodeURIComponent(s.id)

]