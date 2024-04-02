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
                    console.log(data)
                    document.getElementById('email').value = data.Email;
                    document.getElementById('sub-plan').value = data.Subscription;
                    document.getElementById('username').innerHTML = data.Username;
                    document.getElementById('phone_no').value = data.PhoneNumber;
                    document.getElementById('balance').value = data.Balance;
                    document.getElementById('total-bal').value = data.TotalBalance;
                    document.getElementById('avail-balance').value = data.AvailableBalance;
                    document.getElementById('date').value = data.DateJoined;
                    if (data.ActiveStatus == true){
                        document.getElementById('active').checked = true
                    }else{
                        document.getElementById('unactive').checked = true;
                    }
                }
            })
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
    fetch('/admin/get-withdrawwal', {
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
                    console.log(data)
                    let informationheading = document.querySelector('.withdrawal-tab .table-heading')
                    document.querySelector('.withdrawal-tab #id').value = data.id
                    document.querySelector('.withdrawal-tab #avail-balance').value = data.User_avail_balance
                    document.querySelector('.withdrawal-tab #username').innerHTML = data.Username
                    document.querySelector('.withdrawal-tab #usr-email').innerHTML = data.Email
                    document.querySelector('.withdrawal-tab #wallet').value = data.Wallet
                    document.querySelector('.withdrawal-tab #amount').value = data.Amount
                    document.querySelector('.withdrawal-tab #fee').value = data.Fee_charge
                    document.querySelector('.withdrawal-tab #date').value = data.Date
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


