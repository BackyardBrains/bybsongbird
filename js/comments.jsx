import React from 'react';
import PropTypes from 'prop-types';

class Comments extends React.Component {
  /* Display number of likes a like/unlike button for one post
   * Reference on forms https://facebook.github.io/react/docs/forms.html
   */

  constructor(props) {
    // Initialize mutable state
    super(props);
    this.state = { comments: [], newcomment: '' };
    // !!!! Must have these binding calls for the form to work
    this.changeHandler = this.changeHandler.bind(this);
    this.handleKeyPress = this.handleKeyPress.bind(this);
  }

  componentDidMount() {
    // Call REST API to get number of likes
    fetch(this.props.url, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState({
          comments: data.comments,
          newcomment: '',
        });
      })
      .catch(error => console.log(error)); // eslint-disable-line no-console
  }

  // Handles the action of posting comment
  handleKeyPress(event) {
    event.preventDefault();
    fetch(this.props.url,
      {
        credentials: 'same-origin',
        method: 'POST',
        headers: {
          'Content-Type': 'application/json; charset=utf-8',
        },
        body: JSON.stringify({ text: this.state.newcomment }),
      })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState({
          comments: this.state.comments.concat(data),
          newcomment: '',
        });
      })
      .catch(error => console.log(error)); // eslint-disable-line no-console
  }

  changeHandler(event) {
    // console.log('change')
    this.setState(
      { newcomment: event.target.value },
    );
  }

  rendercomment(comment) {
    // must assign key as comment id to avoid key validation
    // called const garbage to avoid warning
    const garbage = this.state.newcomment;
    return (
      <p key={comment.commentid} id={garbage}>
        <a href={comment.owner_show_url}><b>{comment.owner}</b></a> {comment.text}
      </p>
    );
  }

  render() {
    // see this link for map function https://reactjs.org/docs/lists-and-keys.html
    return (
      <div className="comments">
        {this.state.comments.map(comment => (
          this.rendercomment(comment)))
        }

        <form id="comment-form" onSubmit={this.handleKeyPress}>
          <input
            type="text"
            value={this.state.newcomment}
            onChange={this.changeHandler}
          />
        </form>
      </div>
    );
  }
}

Comments.propTypes = {
  url: PropTypes.string.isRequired,
};

export default Comments;
