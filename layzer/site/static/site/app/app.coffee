ng = @angular

slideSpeed = 300
fadeSpeed = 300

m = ng.module 'layzer', ['ngResource',  'input', 'modal']

m.config [
    '$routeProvider'
    ($routeProvider) ->
        $routeProvider.when '/feed/*feed',
            templateUrl: 'feeditems.html'
            controller: 'FeedItemsCtrl'
            resolve:
                feedItems: [
                    'feeditemsservice', '$route',
                    (feeditemsservice,   $route) ->
                        feeditemsservice.getForFeed decodeURIComponent($route.current.params.feed)
                ]
]

getProgress = (e) ->
    progress = e.attr('ng-animate-progress') || e.data('ng-animate-progress')
    scope = e.scope()
    if progress
        -> scope.$apply progress
    else
        ->

m.animation 'slide-down', ->
    setup: (e) -> e.hide()
    start: (e, done) ->
        e.slideDown
            duration: slideSpeed
            done: -> done()
            progress: getProgress e

m.animation 'slide-up', ->
    setup: (e) -> e.show()
    start: (e, done) ->
        e.slideUp
            duration: slideSpeed
            done: -> done()
            progress: getProgress e

m.animation 'fade-in', ->
    setup: (e) -> e.css opacity: 0
    start: (e, done) ->
        e.animate opacity: 1,
            duration: fadeSpeed
            done: -> done()
            progress: getProgress e

m.animation 'fade-out', ->
    setup: (e) -> e.css opacity: 1
    start: (e, done) ->
        e.animate opacity: 0,
            duration: fadeSpeed
            done: -> done()
            progress: getProgress e

m.run [
    '$rootScope',
    ($rootScope) ->
        getAn = (fnIn, fnOut) ->
            enter: fnIn
            leave: fnOut
            show: fnIn
            hide: fnOut

        $rootScope.an =
            slide: getAn 'slide-down', 'slide-up'
            fade: getAn 'fade-in', 'fade-out'
]
