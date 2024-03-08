import React from 'react';
import { Link } from 'react-router-dom';
import CredentialsForm from './CredentialsForm';

function Register() {
    return (
        <div>
            <p>This is the Register Page.</p>
            <Link to="/">Go back homeeee leaveeee</Link>
            <CredentialsForm isRegister={true} />
        </div>
    );
}

export default Register;