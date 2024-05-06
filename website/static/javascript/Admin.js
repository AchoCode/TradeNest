let alertMsg = document.getElementById('alert-msg')
if(alertMsg){
    setTimeout(()=>{
        alertMsg.classList.remove('show')
    },3000)
}
let overlay = document.querySelector('.overlay')

let dates = document.querySelectorAll('.dates')
dates.forEach(date=>{
    console.log(date.textContent)
    const newdate = new Date(date.textContent)
    let options ={
        year: 'numeric', 
        month: 'short', 
        day: 'numeric', 
        hour: 'numeric', 
        minute: 'numeric', 
        second: 'numeric', 
    }

    let formattedDate = newdate.toLocaleDateString('en-US', options)
    date.textContent = formattedDate
})

// ------------------------------------NAVIGATION------------------------------

const tabs = document.querySelectorAll('.tab')
function activeTab(){
    tabs.forEach(tab=>{
        tab.classList.remove('active')
    })
    this.classList.add('active')
}
tabs.forEach(tab=>{
    tab.addEventListener('click', activeTab)
})


// ------------------------dashboard tab------------------------
const dashboardTabLink = document.querySelector('#dashboard')
const dashboardTab = document.querySelector('.dashboard-box')
dashboardTabLink.addEventListener('click', ()=>{
    if (dashboardTabLink.classList.contains('active')){

        dashboardTab.classList.add('online')
        usersTab.classList.remove('online')
        commentsTab.classList.remove('online')
        postTab.classList.remove('online')
        depositTab.classList.remove('online')
        withdrawalTab.classList.remove('online')

    }
})

// ------------------------users tab------------------------
const userTabLink = document.querySelector('#users')
const usersTab = document.querySelector('.users-tab')
userTabLink.addEventListener('click', ()=>{
    if (userTabLink.classList.contains('active')){

        dashboardTab.classList.remove('online')
        usersTab.classList.add('online')
        commentsTab.classList.remove('online')
        postTab.classList.remove('online')
        depositTab.classList.remove('online')
        withdrawalTab.classList.remove('online')

    }
})

let usrCard = document.querySelector('.user-container .card-information')
let tradeDiv = document.querySelector('.users-tab .user-trade')


//for users tab, user form details api
function getUser(usrId) {
    fetch('/admin/get-user', {
        method: 'POST',
        body: JSON.stringify({usrId: usrId}),
    })
    .then(response => {
            if(!response.ok) {
                throw new Error('Network response was not ok');
            }
            // Parse the JSON response
            return response.json();
        })
            .then(data => {
                if (data.error) {
                    alert(data.error);
                } else {

                    if (usrCard.classList.contains('inactive') && tradeDiv.classList.contains('active')){
                            usrCard.classList.remove('inactive')
                            tradeDiv.classList.remove('active')
                    }
                    document.getElementById('email').value = data.Email;
                    document.getElementById('sub-plan').value = data.Subscription;
                    document.getElementById('username').innerHTML = data.Username;
                    document.getElementById('phone_no').value = data.PhoneNumber;
                    document.getElementById('balance').value = data.Balance;
                    document.getElementById('total-bal').value = data.Earnings;
                    document.getElementById('avail-balance').value = data.AvailableBalance;
                    document.getElementById('usr-date').innerHTML = data.DateJoined;
                    if (data.ActiveStatus == true){
                        document.getElementById('active').checked = true
                    }else{
                        document.getElementById('unactive').checked = true;
                    }
                }
            })
}

//for search bar
document.getElementById("search-bar").addEventListener("keyup", function() {
    var searchValue = this.value.toLowerCase();
    var userList = document.querySelectorAll(".user");
  
    userList.forEach(function(user) {
      var name = user.querySelector("h5").textContent.toLowerCase();
      var email = user.querySelector("p i").textContent.toLowerCase();
  
      if (name.includes(searchValue) || email.includes(searchValue)) {
        user.style.display = ""; // Show the user if the search value matches name or email
      } else {
        user.style.display = "none"; // Hide the user if the search value does not match
      }
    });
  });
function setTrade(tradeUsrId){
    fetch('/admin/set-trade',{
        method: 'POST',
        body: JSON.stringify({tradeUsrId:tradeUsrId})
    }).then(response => {
            if(!response.ok) {
                throw new Error('Network response was not ok');
            }
            // Parse the JSON response
            return response.json();
        }).then(data =>{
                    if(data.TradeCount === '0'){
                        document.querySelector('.user-trade #username').innerHTML = data.Username
                        document.querySelector('.user-trade #subscription-plan').innerHTML = data.SubscriptionPlan
                        document.getElementById('trade-balance').value = data.UserBalance
                        document.getElementById('usr-id').value = data.id
                    }else{
                        document.querySelector('.user-trade #username').innerHTML = data.Username
                        document.querySelector('.user-trade #subscription-plan').innerHTML = data.SubscriptionPlan
                        document.getElementById('trade-balance').value = data.UserBalance
                        document.getElementById('usr-id').value = data.id
                    }
                    usrCard.classList.add('inactive')
                    tradeDiv.classList.add('active')
                    let userList = document.querySelectorAll(".user-trade .user");
                            userList.forEach(trade=>{
                                let tradeId = trade.querySelector('.trade-usr-id')
                
                                if(tradeId.value == data.id){
                                    trade.style.display = ''
                                }else{
                                    trade.style.display = 'none'
                                }
                            })
            })


}

function closeTrade(tradeId){
    fetch('/admin/close-trade',{
        method: 'POST',
        body: JSON.stringify({tradeId:tradeId})
    }).then(response => {
        if(!response.ok) {
            throw new Error('Network response was not ok');
        }
        // Parse the JSON response
        return response.json();
    })
    window.location.href = '/admin/dashboard?activepage=user'

}
let deleteUsrId = null;
function deleteNote(usrId, firstname, lastname){
    let deleteNote = document.querySelector('.delete-note')
    let UserName = document.querySelector('#userName')
    
    deleteUsrId = usrId
    overlay.classList.add('blurred')
    deleteNote.classList.add('active')
    UserName.innerHTML = `${firstname} ${lastname}`
}
function continueDelete(){
    if(deleteUsrId != null){
        fetch('/admin/delete-user',{
            method: 'POST',
            body: JSON.stringify({usrId:deleteUsrId})
        }).then(response => {
            if(!response.ok) {
                throw new Error('Network response was not ok');
            }
            // Parse the JSON response
            return response.json()
        }).then(data=>{
            if (data.Status === 'success'){
                window.location.href = '/admin/dashboard?activepage=user'
            }
        })
    }
}
function abortDelete(){
    let deleteNote = document.querySelector('.delete-note')
    let UserName = document.querySelector('#userName')
    
    deleteUsrId = null
    overlay.classList.remove('blurred')
    deleteNote.classList.remove('active')

}
  // ------------------------comments tab------------------------
const commentTabLink = document.querySelector('#comments')
const commentsTab = document.querySelector('.comments-tab')
commentTabLink.addEventListener('click', ()=>{
    if (commentTabLink.classList.contains('active')){

        dashboardTab.classList.remove('online')
        usersTab.classList.remove('online')
        commentsTab.classList.add('online')
        postTab.classList.remove('online')
        depositTab.classList.remove('online')
        withdrawalTab.classList.remove('online')

    }
})

function DeleteComment(commentId){
    fetch('/admin/delete-comment',{
        method: 'POST',
        body: JSON.stringify({commentId:commentId})
    }).then(
        window.location.href = '/admin/dashboard?activepage=comment' 
    )
}
// ------------------------post tab------------------------
const postTabLink = document.querySelector('#post')
const postTab = document.querySelector('.post-tab')
postTabLink.addEventListener('click', ()=>{
    if (postTabLink.classList.contains('active')){

        dashboardTab.classList.remove('online')
        usersTab.classList.remove('online')
        commentsTab.classList.remove('online')
        postTab.classList.add('online')
        depositTab.classList.remove('online')
        withdrawalTab.classList.remove('online')

    }
})

function deletePost(postId){
    fetch('/admin/delete-post', {
        method: 'POST',
        body: JSON.stringify({postId:postId})
    }).then(
        window.location.href = '/admin/dashboard?activepage=post'
    )
}
// ------------------------deposit tab------------------------
const depositTabLink = document.querySelector('#deposit')
const depositTab = document.querySelector('.deposit-tab')
depositTabLink.addEventListener('click', ()=>{
    if (depositTabLink.classList.contains('active')){

        dashboardTab.classList.remove('online')
        usersTab.classList.remove('online')
        commentsTab.classList.remove('online')
        postTab.classList.remove('online')
        depositTab.classList.add('online')
        withdrawalTab.classList.remove('online')

    }
})

function Approve(depositId){
    fetch('/admin/approve-deposit',{
        method: 'POST',
        body: JSON.stringify({depositId:depositId})
    }).then(
        window.location.href =  '/admin/dashboard?activepage=deposit'
    )
}
function Delete(depositId){
    fetch('/admin/delete-deposit',{
        method: 'POST',
        body: JSON.stringify({depositId:depositId})
    }).then(
        window.location.href =  '/admin/dashboard?activepage=deposit'
    )
}
// ------------------------withdrawal tab------------------------
const withdrawalTabLink = document.querySelector('#withdrawal')
const withdrawalTab = document.querySelector('.withdrawal-tab')
withdrawalTabLink.addEventListener('click', ()=>{
    if (withdrawalTabLink.classList.contains('active')){

        dashboardTab.classList.remove('online')
        usersTab.classList.remove('online')
        commentsTab.classList.remove('online')
        postTab.classList.remove('online')
        depositTab.classList.remove('online')
        withdrawalTab.classList.add('online')
    }
})
function getTransaction(TransactionId) {
    fetch('/admin/get-withdrawal', {
        method: 'POST',
        body: JSON.stringify({TransactionId: TransactionId}),
    })
    .then(response => {
            if(!response.ok) {
                throw new Error('Network response was not ok');
            }
            // Parse the JSON response
            return response.json();
        })
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                let informationheading = document.querySelector('.withdrawal-tab .table-heading')
                document.querySelector('.withdrawal-tab #id').value = data.id
                document.querySelector('.withdrawal-tab #with-avail-balance').value = data.User_avail_balance
                document.querySelector('.withdrawal-tab #username').innerHTML = data.Username
                document.querySelector('.withdrawal-tab #usr-email').innerHTML = data.Email
                document.querySelector('.withdrawal-tab #wallet').value = data.Wallet
                document.querySelector('.withdrawal-tab #amount').value = data.Amount
                document.querySelector('.withdrawal-tab #fee').value = data.Fee_charge
                document.querySelector('.withdrawal-tab #with-date').value = data.Date
                let feeCharge = parseFloat(data.Fee_charge)
                let Amount = parseFloat(data.Amount)
                let UserAvailBal = parseFloat(data.User_avail_balance)
                if(feeCharge + Amount >  UserAvailBal){
                    informationheading.style.backgroundColor = 'red'
                }else{
                    informationheading.style.backgroundColor = 'green'
                }
            }
        })
}

//---------------admin dashform------------------

let adminSettings = document.querySelector('.admin-settings');
let gearIcon = document.querySelector('.gear-icon');
let adminContent = document.querySelector('.admin-content');
let closeIcon = document.querySelector('.admin-content .icon')

gearIcon.addEventListener('click',()=>{
    adminSettings.classList.remove('inactive')
    gearIcon.classList.remove('active')
    overlay.classList.add('blurred')
    setTimeout(()=>{
        adminContent.classList.remove('inactive')
    },300)
})

closeIcon.addEventListener('click', ()=>{
    adminSettings.classList.add('inactive')
    gearIcon.classList.add('active')
    adminContent.classList.add('inactive')
    overlay.classList.remove('blurred')


})