;(function (ng) {
	ng.module('layzer').filter('uriencode', function () {
		return function (input) {
			return encodeURIComponent(input);
		}
	});
}(angular));
