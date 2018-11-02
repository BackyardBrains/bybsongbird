import React from 'react';
import PropTypes from 'prop-types';

class Sample extends React.Component {
  /* Display audio samples
   * Reference on forms https://facebook.github.io/react/docs/forms.html
   */

  constructor(props) {
    // Initialize mutable state+
    super(props);
    this.state = {
    };
  }

  componentDidMount() {
    // Call REST API to get a post
    fetch(this.props.url, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        // alert(data.results[1].url);
        this.setState({
        });
      })
      .catch(error => console.log(error)); // eslint-disable-line no-console
  }

  render() {
    return (
      <p>hello you {this.context.options}</p>
    );
  }
}

Sample.propTypes = {
  url: PropTypes.string.isRequired,
};

export default Sample;
