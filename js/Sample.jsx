import React from 'react';
import {Link} from 'react-router-dom';
import PropTypes from 'prop-types';

class Sample extends React.Component {
  /* Display audio samples
   * Reference on forms https://facebook.github.io/react/docs/forms.html
   */

  constructor(props) {
    // Initialize mutable state+
    super(props);
    this.state = {
      results: [],
    };
  }

  componentDidMount() {
    // Call REST API to get a sample
    fetch(this.props.url, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState({
          results: data.results,
        });
      })
      .catch(error => console.log(error)); // eslint-disable-line no-console
  }

  renderSample(result){
    let circleName = "c100";
    circleName = circleName + " " + "p" + result.perR + " " + result.color;
    let imgurl = "/static/songs/users/users_clean/" + result.id + ".png";
    return (
      <div className="sample" key={result.id}>
        <div className="circles">
          <div className={circleName}>
            <span>{result.per + "%"}</span>
            <div className="slice">
              <div className="bar"></div>
              <div className="fill"></div>
            </div>
          </div>
        </div>

        <div className="species">Species:</div>
        <div className="bird">{result.type}</div>
        <div className="upload">Upload On:</div>
        <div className="time">{result.date}</div>

        <div><img src={imgurl} className="wav"/></div>
        <form action="/info">
          <button type="submit" name="sampleid" value={result.id} className="button">Learn More</button>
        </form>
      </div>
    );
  }

  render() {
    return (
      <div>
        {this.state.results.map(result => (
          this.renderSample(result)))
        }
      </div>
    );
  }
}

Sample.propTypes = {
  url: PropTypes.string.isRequired,
};

export default Sample;
