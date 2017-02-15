import React from 'react';
import ReactDOM from 'react-dom';

var token = document.head.querySelector("[name=token]").content,
    user = {};

var Profile = React.createClass({
  render: function() {
    return (
      <div className="profile__info">
         <h3>{user.first_name} {user.last_name}</h3>
         <h4>{user.email}</h4>
      </div>
    );
  }
});

var App = React.createClass({
  render: function() {
    return (
      <div className="app">
        <ol className="breadcrumb">
          <li>Профиль</li>
        </ol>
        <Profile data={user}/>
      </div>
    );
  }
});

fetch('/api/profile/?token=' + token)
  .then(
    function(response) {
      response.json().then(function(data) {
        user = data['users'];
        ReactDOM.render(
            <div className="col-md-6"><App /></div>,
            document.getElementById('profile')
          );
      });
    }
  )
  .catch(function(err) {
    console.log('Fetch Error :-S', err);
    return false;
});
