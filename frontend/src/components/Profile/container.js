import React, { Component } from "react";
import PropTypes from "prop-types";
import Explore from "./presenter";

class Container extends Component {
  state = {
    loading: true
  };
  static propTypes = {
    getProfile: PropTypes.func.isRequired,
  };
  componentDidMount() {
    const { getProfile } = this.props;
    if (!this.props.userList) {
      getProfile();
    } else {
      this.setState({
        loading: false
      });
    }
  }
  componentWillReceiveProps = nextProps => {
    if (nextProps.userList) {
      this.setState({
        loading: false
      });
    }
  };
  render() {
    const { userList } = this.props;
    return <Explore {...this.state} userList={userList} />;
  }
}

export default Container;