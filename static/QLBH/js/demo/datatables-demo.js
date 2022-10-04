// Call the dataTables jQuery plugin


// $(document).ready(function() {
//   $('#dataTables').DataTable();
// });
//
$(document).ready(function() {
  // $('#dataTable-all').DataTable();
  let xlist = document.querySelectorAll("#myTab li a");
  for (let item of xlist) {
    let xid = item.getAttribute('aria-controls')
    console.log(xid);
    $('#dataTable-' + xid).DataTable();
  }
});

