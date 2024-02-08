import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { login } from './AuthService.ts';
import { useForm } from 'react-hook-form';


/**
 * TODO: redirect when logged in
 */
function Login() {
    const navigate = useNavigate();
    const { register, handleSubmit, formState: { errors }} = useForm();

    return (
        <form onSubmit={handleSubmit(async (data) => {
            await login(data)
                .then(() => navigate('/'))
                .catch(e => {
                    alert('Login Failed');
                    console.error(e);
                })
        })}>
            <div>
                email: <input
                    {...register(
                        'email',
                        { required: true })}
                    placeholder='abc@datedive.com' />
            </div>
            <div>
                password: <input
                    {...register(
                        'password',
                        { required: true })}
                    type='password' placeholder='******' />
            </div>           
            <button type='submit'>
                login
            </button>
        </form>
    )
}

export default Login;