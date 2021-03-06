ng = @angular

m = ng.module 'input', []

m.directive 'inputOnEscape', ->
  (scope, element, attrs) ->
    handler = (e) ->
      scope.$apply attrs.inputOnEscape
    element.on 'keydown.keys', handler

    removeOn = scope.$on '$destroy', ->
      element.off 'keydown.keys', handler
      removeOn()

m.directive 'autoFocus', [
  '$timeout'
  ($timeout) ->
    link: (scope, element, attrs) ->
      e = element[0]
      scope.$watch attrs.autoFocus, (value) ->
        $timeout ->
          if value
            e.focus()
            e.select()
          else
            e.blur()
    priority: -10000
]
