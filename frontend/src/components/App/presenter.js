import React from 'react';
import PropTypes from "prop-types";
import { Route, Switch } from "react-router-dom";
import "./styles.scss";
import Auth from "components/Auth";
import Footer from "components/Footer";
import Navigation from "components/Navigation";
import Feed from "components/Feed";
import Explore from "components/Explore";
import Profile from "components/Profile";
import Search from "components/Search";

const App = props => [
    props.isLoggedIn ? <Navigation key={1} /> : null,
    props.isLoggedIn ? <PrivateRoutes key={2} /> : <PublicRoutes jey={2} />,
    <Footer ke={3} />
];

App.propTypes = {
    isLoggedIn:PropTypes.bool.isRequired
};

const PrivateRoutes = props => (
    <Switch>
        <Route exact path="/" component={Feed} />
        <Route path="/explore" component={Explore} />
        <Route path="/profile" component={Profile} />
        <Route path="/search/:searchTerm" render={() => "search"} />
    </Switch>
)
const PublicRoutes = props => (
    <Switch>
        <Route exact path="/" component={Auth} />
        <Route exact path="/forgot" component={Search} />
    </Switch>
)

export default App;