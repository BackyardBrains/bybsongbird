import React from 'react';
import ReactDOM from 'react-dom';
import Sample from './Sample';
import {BrowserRouter as Router, Route} from "react-router-dom";

ReactDOM.render(
  (
    <Router>
      <Route path="/" component={sample}/>
    </Router>
  ),
  document.getElementById("reactEntry"),);

function sample(){
  return (<Sample url="/api/index"/>);
}