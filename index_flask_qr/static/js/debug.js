// stan 2018-08-04


// $.fn.serializeObject = function() {
//   var o = {};
//   var a = this.serializeArray();
//   $.each(a, function() {
//     if (o[this.name] !== undefined) {
//       if (!o[this.name].push) {
//         o[this.name] = [o[this.name]];
//       }
//       o[this.name].push(this.value || '');
//     } else {
//       o[this.name] = this.value || '';
//     }
//   });
//   return o;
// };


// https://codepen.io/seriema/pen/nupEJ
jQuery.fn.serializeObject = function () {
  var formData = {};
  var formArray = this.serializeArray();

  for(var i = 0, n = formArray.length; i < n; ++i)
    formData[formArray[i].name] = formArray[i].value;

  return formData;
};
