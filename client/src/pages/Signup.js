import { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { koreaLocation } from '../constants/constants';

function Signup() {
    const emailRegEx = /^[A-Za-z0-9]([-_.]?[A-Za-z0-9])*@[A-Za-z0-9]([-_.]?[A-Za-z0-9])*\.[A-Za-z]{2,3}$/;
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [nickname, setNickname] = useState('');
    const [gender, setGender] = useState('');
    const [location, setLocation] = useState('시/도');
    const [subLocation, setSubLocation] = useState('');
    const [checkbox1, setCheckbox1] = useState(false);
    const [checkbox2, setCheckbox2] = useState(false);
    const navigate = useNavigate();

    const emailCheck = (email) => {
        return emailRegEx.test(email);
    }
    const onChangeEmail = (e) => {
        setEmail(e.target.value);
    };
    const onChangePassword = (e) => {
        setPassword(e.target.value);
    };
    const onChangeNickname = (e) => {
        setNickname(e.target.value);
    };
    const onLocationChange = (e) => {
        setLocation(e.target.value);
        setSubLocation('');
    };
    const onSubLocationChange = (e) => {
        setSubLocation(e.target.value);
    };
    const checkHandler = ({ target }) => {
        if (target.id === 'male') {
            if (target.checked) {
                setGender('male');
                setCheckbox1(true);
                setCheckbox2(false);
            } else {
                setGender('');
                setCheckbox1(false);
            }
        } else {
            if (target.checked) {
                setGender('female');
                setCheckbox1(false);
                setCheckbox2(true);
            } else {
                setGender('');
                setCheckbox2(false);
            }
        }
    }

    async function handleSubmit() {
        try {
            if (emailCheck(email)) {
                const response = await axios.post('/api/user/signup', {
                    email: email,
                    password: password,
                    nickname: nickname,
                    gender: gender,
                    location: location + ' ' + subLocation
                }
                )
                navigate('/');
            }
        } catch (error) {
            console.log(error);
        }
    };

    return (
        <div>
            <div>
                email: <input onChange={onChangeEmail} value={email} />
            </div>
            <div>
                password: <input onChange={onChangePassword} value={password} />
            </div>
            <div>
                nickname: <input onChange={onChangeNickname} value={nickname} />
            </div>
            <div>
                gender:
                <input id='male' onChange={checkHandler} checked={checkbox1} type="checkbox" /> Male
                <input id='female' onChange={checkHandler} checked={checkbox2} type="checkbox" /> Female
            </div>
            <div>
                location: <select onChange={onLocationChange}>
                    {Object.keys(koreaLocation).map((division) => (
                        <option key={division} value={division}>
                            {division}
                        </option>
                    ))}
                </select>
                <select onChange={onSubLocationChange}>
                    {koreaLocation[location].map((subDivision) => (
                        <option key={subDivision} value={subDivision}>
                            {subDivision}
                        </option>
                    ))}
                </select>
            </div>
            <div>
                <button onClick={handleSubmit}>
                    signup
                </button>
            </div>
        </div>
    )
}

export default Signup;