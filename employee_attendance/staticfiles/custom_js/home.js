$(document).ready(function(){    
    initTable({});
});


function initTable(data) {
/**
 * This function is used to view table.
 *  
 */

$('#mytable').DataTable({
    
    "aaSorting": [],
    "processing": true,
    "serverSide": true,    
    "columnDefs": [
            { orderable: false, targets: 0 },
            { orderable: false, targets: 5 },
            { orderable: false, targets: 6 }            
        ],
    "columns": [                    
        {'data': 'srno', 'title': 'Sr.No.', "sClass": 'text-center'},
        {'data': 'employee_name', 'title': 'Employee Name', "sClass": 'text-center'},               
        {'data': 'in_time', 'title': 'IN Time', "sClass": 'text-center'},
        {'data': 'out_time', 'title': 'OUT Time', "sClass": 'text-center'},
        {'data': 'status', 'title': 'Status', "sClass": 'text-center'},
        {'data': 'in_btn', 'title': 'IN', "sClass": 'text-center'},
        {'data': 'out_btn', 'title': 'OUT', "sClass": 'text-center'}
    ],
    dom: 'Bfrtip',
    "ajax":{
        type: "POST",
        url:"/api/employee_list/",
        data: function(d){           
            d.csrfmiddlewaretoken=  getCookie('csrftoken');            
            d.date = data.date;
        },        
        dataFilter: function(response){
            var temp = JSON.parse(response);            
            $('.present_emp').text(`Present Employee:${temp.present_emp}`)
            $('.absent_emp').text(`Absent Employee:${temp.absent_emp}`)
            return response;

        },
        error:function(data){
            
        }
    },
    destroy: true,            
    lengthChange: true,
   
})
}


$(document).on('click','#btn_submit',function(){

    $(".clear_span").text('');
    var element = $(this);
    $(element).prop('disabled', true);
    $(element).html('<i class="fa fa-spinner fa-spin"></i> Processing');

    var form = new FormData($('#add_employee')[0]);

    $.ajax({
        type:"POST",
        processData: false,
        contentType: false,
        url:"/api/add_employee/",
        data:form,
        success:function(response){

            $.confirm({
                title: 'Success',
                content: 'User saved successfully !',
                type: 'green',
                typeAnimated: true,
                buttons: {
                    tryAgain: {
                        text: 'OK',
                        btnClass: 'btn-green',
                        action: function(){
                            location.reload()
                        }
                    },
                   
                }
            });



            $(element).prop('disabled', false);
            $(element).html('Save');
        },
        error:function(err){
            $.each(err.responseJSON, function (idx, val) {                
                $("#add_employee").find(`.${idx}_error`).html(val[0]);
            });         
            $(element).prop('disabled', false);
            $(element).html('Save');
        }
    })
})




$(document).on('click','.in_btn_class',function(){
    var element = $(this)
    setTime(element,'INTIME')

})

$(document).on('click','.out_btn_class',function(){
        var element = $(this)
        setTime(element,'OUTTIME')
})

function setTime(element,flag){

    $(element).prop('disabled', true);
    $(element).html('<i class="fa fa-spinner fa-spin"></i> Processing');

    let user_id = $(element).data('id')
    data = {
        'user_id':user_id,
        'flag':flag,
        'csrfmiddlewaretoken': getCookie('csrftoken')
    }

    $.ajax({
        type:"POST",
        url:"/update_time/",
        data:data,
        success:function(response){
            console.log(response)

            toastr["success"](`Employee ${response.time_status} updated.`);
                        toastr.options = {
                            closeButton: true,
                            debug: false,
                            newestOnTop: true,
                            progressBar: true,
                            positionClass: "toast-top-right",
                            preventDuplicates: false,
                            onclick: null,
                            showDuration: "300",
                            hideDuration: "1000",
                            timeOut: "5000",
                            extendedTimeOut: "1000",
                            showEasing: "swing",
                            hideEasing: "linear",
                            showMethod: "fadeIn",
                            hideMethod: "fadeOut"
            }
            initTable({})

            
        },
        error:function(err){

            if (err.status == 500) {
                $.confirm({
                  title: "Encountered an error!",
                  content: "Something went wrong ! Please contact techinical team.",
                  type: "red",
                  typeAnimated: true,
                  buttons: {
                    tryAgain: {
                      text: "Try again",
                      btnClass: "btn-red",
                      action: function () {
                        location.reload();
                      },
                    },
                  },
                });
              }else{
                  

                    $.each(err.responseJSON,function(idx,val){

                        toastr["error"](val);
                        toastr.options = {
                            closeButton: true,
                            debug: false,
                            newestOnTop: true,
                            progressBar: true,
                            positionClass: "toast-top-right",
                            preventDuplicates: false,
                            onclick: null,
                            showDuration: "300",
                            hideDuration: "1000",
                            timeOut: "5000",
                            extendedTimeOut: "1000",
                            showEasing: "swing",
                            hideEasing: "linear",
                            showMethod: "fadeIn",
                            hideMethod: "fadeOut"
                        }

                    })

                  

                    initTable({})


        }
    }
    })

}



$(document).on('click', '#filter', function () {

    let obj_data = {}

    date = $('#date_data').val()

    if (date) {
        obj_data.date = date
    }


    initTable(obj_data)

})


$(document).on('click','#export_pdf_link',function(){


    let obj_data = {}

    date = $('#date_data').val()

    if (date) {
        obj_data.date = date
    }else{
        obj_data.date = new Date().getTime() / 1000;
    }


    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/x-www-form-urlencoded");
    myHeaders.append("X-CSRFToken", getCookie('csrftoken'));
    var searchParams = new URLSearchParams(obj_data);


    fetch("/api/export_pdf/",
{
    method: "POST",
    headers: myHeaders,
    body: searchParams
})
.then(resp => resp.blob())
.then(blob => {
    const url = window.URL.createObjectURL(blob);
    
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;        
        a.download = 'employee.pdf';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);


 }).catch(e => console.log("e", e));




})