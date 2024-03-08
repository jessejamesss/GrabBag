import React from 'react';
import { Link } from 'react-router-dom';

function Home() {
    return (
        <div>
            <h1>Home Page !!!</h1>
            <Link to="/register">Register NOWWWWW!</Link>
            <Link to="/login">please please please login</Link>
        </div>
    )
}

export default Home;