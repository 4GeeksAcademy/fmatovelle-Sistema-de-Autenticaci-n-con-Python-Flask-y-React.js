import React, { useState } from 'react';
import axios from 'axios';  
import { useNavigate } from 'react-router-dom'; 

const SignupForm = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const navigate = useNavigate();  

    // Handle form submission
    const handleSubmit = async (e) => {
        e.preventDefault();  

        try {
            const response = await axios.post('https://musical-eureka-976gv99g474vfpwp6-3001.app.github.dev/api/signup', {  // Update with the correct backend URL
                email: email,
                password: password
            });
            

            console.log('Signup response:', response);  

            if (response.status === 201) {  
                setSuccess('User created successfully!');
                setError('');

                navigate('/login');  
            }
        } catch (err) {
            console.error('Signup error:', err);  

            if (err.response && err.response.data) {
                setError(err.response.data.message);
            } else {
                setError('An error occurred. Please try again.');
            }
            setSuccess('');
        }
    };

    return (
        <div className="container d-flex justify-content-center align-items-center" style={{ minHeight: '80vh' }}>
            <div className="card p-4 shadow" style={{ maxWidth: '400px', width: '100%' }}>
                <h2 className="text-center mb-4">Sign Up</h2>
                <form onSubmit={handleSubmit}>
                    <div className="mb-3">
                        <label htmlFor="exampleInputEmail1" className="form-label">Email address</label>
                        <input
                            type="email"
                            className="form-control"
                            id="exampleInputEmail1"
                            aria-describedby="emailHelp"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                        <div id="emailHelp" className="form-text">
                            We'll never share your email with anyone else.
                        </div>
                    </div>
                    <div className="mb-3">
                        <label htmlFor="exampleInputPassword1" className="form-label">Password</label>
                        <input
                            type="password"
                            className="form-control"
                            id="exampleInputPassword1"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </div>
                    <button type="submit" className="btn btn-primary w-100">Submit</button>
                    {error && <p className="text-danger mt-3">{error}</p>}
                    {success && <p className="text-success mt-3">{success}</p>}
                </form>
            </div>
        </div>
    );
};

export default SignupForm;
