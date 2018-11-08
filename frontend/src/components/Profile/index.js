import { connect } from "react-redux";
import { actionCreators as userActions } from "redux/modules/user";
import Container from "./container";

const mapDispatchToProps = (dispatch, ownProps) => {
  const { user } = ownProps;
  return {
    getExplore: () => {
      dispatch(userActions.getProfile(user.id));
    }
  };
};

export default connect(null, mapDispatchToProps)(Container);