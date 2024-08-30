import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const Protected = () => {
    const navigate = useNavigate();

    useEffect(() => {
        const token = sessionStorage.getItem("token");

        if (!token) {
            navigate('/login');
        }
    }, [navigate]); 

    return (
        <div>
            <h1>This is the protected route!</h1>
        </div>
    );
};

export default Protected;
