;(function (ng) {
    "use strict";

    ng.module('modal', []).directive('modalWindow', ['$compile', '$timeout', function ($compile, $timeout) {
        var modalScopeAttrs = ['close', 'header', 'submit', 'cancel', 'okText', 'cancelText', 'hideCancel'];
        var modal = ng.element(
            '<div class="modal-backdrop" ng-click="{{modal.cancel}};{{modal.close}}"></div>' +
            '<form class="modal" ng-submit="{{modal.close}}" name="modalForm" novalidate>' +
                '<div class="modal-header">' +
                    '<button type="button" class="close" ng-click="{{modal.cancel}};{{modal.close}}"><i class="icon-remove"></i></button>' +
                    '<h3>{{modal.header}}</h3>' +
                '</div>' +
                '<div class="modal-body">' +
                '</div>' +
                '<div class="modal-footer">' +
                    '<button class="btn btn-large btn-primary" ng-click="{{modal.submit}}" ng-disabled="modalForm.$invalid"><i class="icon-ok"></i> {{modal.okText || \'OK\'}}</button>' +
                    '<button class="btn btn-large" ng-hide="{{modal.hideCancel}}" ng-click="{{modal.cancel}}"><i class="icon-remove"></i> {{modal.cancelText || \'Cancel\'}}</button>' +
                '</div>' +
            '</form>'
        );

        return {
            scope: true,
            compile: function (element) {
                var modalClone = modal.clone(),
                    children = element.children(),
                    body = modalClone.find('.modal-body');
                body.append(children);
                element.append(modalClone);
                return {
                    pre: function (scope, element, attrs) {

                        var modalModel = {};
                        ng.forEach(modalScopeAttrs, function(value) {
                            modalModel[value] = attrs[value] || '';
                        });

                        ng.extend(scope, {
                            modal: modalModel
                        });

                    }
                }
            }
        };
    }]);
}(angular));
