ng = @angular
m =  ng.module('layzer')
m.directive 'lzScrollIntoView', ->
    link: (scope, element, attrs) ->
        scrollIntoView = -> element[0].scrollIntoView true

        scope.scrollIntoView = scrollIntoView
        scope.$watch attrs.lzScrollIntoView, (value) ->
            scrollIntoView() if value

m.directive 'lzScrolledToBottom', ->
    (scope, element, attrs) ->
        e = element[0]
        element.scroll ->
            scope.$apply attrs.lzScrolledToBottom if e.offsetHeight + e.scrollTop >= e.scrollHeight
        null
