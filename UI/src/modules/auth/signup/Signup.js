import React, { useState } from 'react';

import { ReactComponent as AppLogo } from "../../../assets/hux-logo-colored.svg";
import SideImage from '../../../assets/login-background.png';
import "./signup.scss";

const Signup = () => {
    const [fullname, setFullname] = useState('');
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [confirmpassword, setConfirmPassword] = useState('');
    const [passwordMatch, setPasswordMatch] = useState(false);
    const [isLengthSufficient, setisLengthSufficient] = useState(false);
    const [containsLowerCase, setcontainsLowerCase] = useState(false);
    const [containsUpperCase, setcontainsUpperCase] = useState(false);
    const [containsNumber, setcontainsNumber] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
  };

  const handleFullnameChange = (e) => {
    setFullname(e.target.value);
  };

  const handleUsernameChange = (e) => {
    setUsername(e.target.value);
  };

  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
    setisLengthSufficient(e.target.value.length>=8);
    setcontainsLowerCase( /.*[a-z]/.test(e.target.value) );
    setcontainsUpperCase( /.*[A-Z]/.test(e.target.value) );
    setcontainsNumber( /.*\d/.test(e.target.value) );
  };

  const handleConfirmPasswordChange = (e) => {
    setConfirmPassword(e.target.value);
    setPasswordMatch(password===confirmpassword);
  };

  return (
    <div>
        <div className='col-sm-12 col-md-7 col-xl-7 col-lg-7'>
            <div className='signup-form'>
                <div>
                    <AppLogo />
                </div>
                <div>
                    <h1>Elevate your <span className='human-bolded'>human</span> experience</h1>
                </div>
                <div className='pb-4'>
                    <h5>Create a HUX account as your first step to reinventing 
                        your marketing, sales, and service capabilities. 
                    </h5>
                </div>
                <div>
                    <form onSubmit={handleSubmit} className='pb-4'>
                        <div className='pb-4'>
                            <label>
                            <div>
                                Full Name
                            </div>
                            <input
                                id="fullname" type="text"
                                value={fullname} autoComplete="true"
                                onChange={handleFullnameChange} />
                            </label>
                        </div>
                        <div className='pb-4'>
                            <label>
                            <div>
                                Email
                            </div>
                            <input
                                id="email" type="text"
                                value={username} autoComplete="true"
                                onChange={handleUsernameChange} />
                            </label>
                        </div>
                        <div className='pb-4'>
                            <label>
                            <div>
                                Password
                            </div>
                            <input
                                id="password" type="password"
                                value={password} autoComplete="true"
                                onChange={handlePasswordChange} />
                            </label>
                        </div>
                        <div className={isLengthSufficient?'text-success':'text-muted'}>
                            At least 8 characters—the more characters, the better!
                        </div>
                        <div className={containsLowerCase?'text-success':'text-muted'}>
                            A least 1 lower case letter (a,b,c...)
                        </div>
                        <div className={containsUpperCase?'text-success':'text-muted'}>
                            At least 1 upper case letter (A,B,C...)
                        </div>
                        <div className={containsNumber?'text-success':'text-muted'}>
                            At least 1 number (1,2,3...)
                        </div>
                        <div className='pb-4'>
                            <label>
                            <div>
                                Confirm Password
                            </div>
                            <input
                                id="confirm-password" type="password"
                                value={confirmpassword} autoComplete="true"
                                onChange={handleConfirmPasswordChange} />
                            </label>
                        </div>
                    <div>
                        <input className='login-btn' id="submit" type="submit" value="Log In" />
                    </div>
                    </form>
                </div>
            </div>
        </div>
        <div className='hidden-xs hidden-sm col-md-5 col-xl-5 col-lg-5 p-0'>
            <img className='signup_background' src={SideImage} alt="Logo" />
        </div>
    </div>
  );
};
export default Signup; 