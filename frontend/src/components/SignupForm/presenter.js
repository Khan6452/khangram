import React from "react";
import PropTypes from "prop-types";
import FacebookLogin from "react-facebook-login";
import formStyles from "shared/formStyles.scss";

const SignupForm = props => (
    <div className={formStyles.formComponent}>
        <h3 className={formStyles.signupHeader}>
            친구들의 사진과 동영상을 보려면 가입하세요.
        </h3>
        <FacebookLogin
            appId="2138424633102143"
            autoLoad={false}
            fields="name,email,picture"
            callback={props.handleFacebookLogin}
            cssClass={formStyles.facebookLink}
            icon="fa-facebook-official"
            textButton="Log in with Facebook"
        />
        <span className={formStyles.divider}>또는</span>
        <form className={formStyles.form} onSubmit={props.handleSubmit}>
            <input 
                type="email" 
                placeholder="Email" 
                className={formStyles.textInput} 
                value={props.emailValue} 
                onChange={props.handleInputChange} 
                name="email" 
            />
            <input 
                type="text" 
                placeholder="Full name" 
                className={formStyles.textInput} 
                value={props.namelValue} 
                onChange={props.handleInputChange} 
                name="name" 
            />
            <input 
                type="username" 
                placeholder="Username" 
                className={formStyles.textInput} 
                value={props.usernameValue} 
                onChange={props.handleInputChange} 
                name="username" 
            />
            <input type="password" placeholder="Password" className={formStyles.textInput} value={props.passwordValue} onChange={props.handleInputChange} name="password" />
            <input type="submit" value="Sign up" className={formStyles.button}/>
        </form>
        <p className={formStyles.terms}>
            By signing up, you agree to our <span>Terms & Privacy Policy</span>
        </p>
    </div>
);

SignupForm.propTypes = {
    handleInputChange: PropTypes.func.isRequired,
    emailValue: PropTypes.string.isRequired,
    nameValue: PropTypes.string.isRequired,
    usernameValue: PropTypes.string.isRequired,
    passwordValue: PropTypes.string.isRequired,
    handleSubmit: PropTypes.func.isRequired,
};

SignupForm.contextTypes = {
    t: PropTypes.func.isRequired
};

export default SignupForm;