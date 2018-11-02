import React from 'react';
import ReactDOM from 'react-dom';
import Sample from './Sample';

ReactDOM.render(
  <Sample url="/api/index" />,
  document.getElementById("reactEntry"),
);
