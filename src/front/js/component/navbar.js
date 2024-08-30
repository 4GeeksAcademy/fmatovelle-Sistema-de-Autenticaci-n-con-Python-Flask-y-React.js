import React from "react";
import { Link, useNavigate } from "react-router-dom";  

export const Navbar = () => {
    const navigate = useNavigate();  

    // Logout function
    const handleLogout = () => {
        sessionStorage.removeItem("token");

        navigate("/login");
    };

    return (
        <nav className="navbar navbar-light bg-light mb-3">
            <Link to="/" className="navbar-brand mb-0 h1">
                React App
            </Link>
            <div className="ml-auto">
                {!sessionStorage.getItem("token") ? (
                    <>
                        <Link to="/signup">  
                            <button className="btn btn-primary mx-2">Sign Up</button>
                        </Link>
                        <Link to="/login">
                            <button className="btn btn-secondary mx-2">Login</button>
                        </Link>
                    </>
                ) : (
                    <button className="btn btn-danger" onClick={handleLogout}>
                        Logout
                    </button>
                )}
            </div>
        </nav>
    );
};
