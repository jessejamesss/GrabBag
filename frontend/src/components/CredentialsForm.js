import React, { useState } from 'react';

function CredentialsForm({ isRegister }) {
    // Set states for register & login fields.
    const [firstName, setFirstName] = useState("");
    const [lastName, setLastName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    // onSubmit function for the CredentialsForm.
    const handleSubmitForm = async (e) => {
        e.preventDefault();

        const credentialsData = {
            firstName,
            lastName,
            email,
            password
        };

        // Construct API enpoint request.
        const registerEndpoint = "http://127.0.0.1:5000/" + (isRegister ? "register" : "login");
        console.log(registerEndpoint);
        const options = {
            method : isRegister ? "POST" : "GET",
            headers :  {
                "Content-Type" : "application/json"
            },
            body : JSON.stringify(credentialsData)
        };

        // Try hitting API endpoint.
        try {
            const response = await fetch(registerEndpoint, options);
            console.log(response.message);
        } catch (error) {
            console.error("Fetch Error: ", error.message);
        }
    };

    return (
        <form onSubmit={handleSubmitForm}>
            { isRegister && ( 
                <div>
                    <label htmlFor="firstName">First Name:</label>
                    <input type="text" id="firstName" value={firstName} onChange={(e) => setFirstName(e.target.value)} required />
                </div>
            )}
            { isRegister && (
                <div>
                    <label htmlFor="lastName">Last Name:</label>
                    <input type="text" id="lastName" value={lastName} onChange={(e) => setLastName(e.target.value)} required />
                </div>
            )}
            <div>
                <label htmlFor="email">Email:</label>
                <input type="text" id="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
            </div>
            <div>
                <label htmlFor="password">Password:</label>
                <input type="text" id="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
            </div>
            <button type="submit">{ isRegister ? "Register" : "Login" }</button>
        </form>
    );
}

export default CredentialsForm;