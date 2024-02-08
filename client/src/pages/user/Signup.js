import { useNavigate } from 'react-router-dom';
import { koreaLocation } from '../../constants/constants';
import { signup } from './AuthService.ts';
import { useForm } from 'react-hook-form';

function Signup() {
    const navigate = useNavigate();
    const { register, handleSubmit, watch, formState: { errors }} = useForm()
    const mainlocation = watch('mainlocation')

    return (
        <form onSubmit={handleSubmit(async (data) => {
            await signup({ ...data, location: data.mainlocation + ' ' + data.sublocation})
                .then(() => navigate('/login'))
                .catch((e) => {
                    alert(`Signup failed: ${e.message}`)
                    console.error(e);
                });
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
            <div>
                nickname: <input
                    {...register(
                        'nickname',
                        { required: true })}
                />
            </div>
            <div>
                gender: <select
                    {...register(
                        'gender',
                        { required: 'Select your gender' },
                    )}>
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                </select>
            </div>
            <div>
                location: <select
                    {...register(
                        'mainlocation',
                        { required: 'Select your primary location' },
                    )}>
                    {Object.keys(koreaLocation).map((division) => (
                        <option key={division} value={division}>
                            {division}
                        </option>
                    ))}
                </select>
                <select
                    {...register('sublocation')}>
                    {koreaLocation[mainlocation]?.map((subDivision) => (
                        <option key={subDivision} value={subDivision}>
                            {subDivision}
                        </option>
                    ))}
                </select>
            </div>
            <div>
                <button type='submit'>
                    signup
                </button>
            </div>
        </form>
    )
}

export default Signup;