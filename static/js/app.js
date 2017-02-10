var token = document.head.querySelector("[name=token]").content,
    user_data = {};

var Profile = React.createClass({
  render: function() {
    return (
      <div className="profile__info">
         <h4><strong>Имя:</strong>  {user_data.first_name} </h4>
         <h4><strong>Фамилия:</strong>  {user_data.last_name}</h4>
         <h4><strong>Email:</strong>  {user_data.email}</h4>
      </div>
    );
  }
});

var App = React.createClass({
  render: function() {
    return (
      <div className="app">
        <div class="page-header">
            <h1>Профиль</h1>
        </div>
        <Profile data={user_data}/>
      </div>
    );
  }
});

fetch('/api/profile/?token=' + token)
  .then(
    function(response) {
      response.json().then(function(data) {
        user_data = data['users'];
        ReactDOM.render(
            <App />,
            document.getElementById('profile')
          );
      });
    }
  )
  .catch(function(err) {
    console.log('Fetch Error :-S', err);
    return false;
});
