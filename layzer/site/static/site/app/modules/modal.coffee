ng = @angular

ng.module('modal', []).directive 'modalWindow', ->
  modalScopeAttrs = ['close', 'header', 'submit', 'cancel', 'okText', 'cancelText', 'hideCancel']
  modal = ng.element """
    <div class="modal-backdrop" ng-click="{{modal.cancel}};{{modal.close}}"></div>
      <form class="modal" ng-submit="{{modal.close}}" name="modalForm" novalidate>
        <div class="modal-header">
          <button type="button" class="close" ng-click="{{modal.cancel}};{{modal.close}}"><i class="icon-remove"></i></button>
          <h3>{{modal.header}}</h3>
        </div>
        <div class="modal-body">
        </div>
        <div class="modal-footer">
          <button class="btn btn-large btn-primary" ng-click="{{modal.submit}}" ng-disabled="modalForm.$invalid"><i class="icon-ok"></i> {{modal.okText || 'OK'}}</button>
          <button class="btn btn-large" ng-hide="{{modal.hideCancel}}" ng-click="{{modal.cancel}}"><i class="icon-remove"></i> {{modal.cancelText || 'Cancel'}}</button>
        </div>
      </form>
    </div>
  """

  scope: true
  compile: (element) ->
    modalClone = modal.clone()
    children = element.children()
    body = modalClone.find '.modal-body'

    body.append children
    element.append modalClone

    pre: (scope, element, attrs) ->
      modalModel = {}
      ng.forEach modalScopeAttrs, (value) ->
        modalModel[value] = attrs[value] || ''
      ng.extend scope,
        modal: modalModel
