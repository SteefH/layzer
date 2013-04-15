
angular.module('layzer').filter 'uriencode', ->
  (input) ->
    encodeURIComponent input
