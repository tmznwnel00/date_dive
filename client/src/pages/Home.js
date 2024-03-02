import axios from 'axios'
import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom';
import { ACCESS_TOKEN } from './user/AuthService.ts';
import { Button } from '@mui/material';


export default function Home() {
  const navigate = useNavigate();
  const [match, setMatch] = useState()

  useEffect(() => {
    axios.get('/api/match/new').then(x => {
      setMatch(x.data);
    }).catch(e => {
      navigate('/login')
    })
  }, []);

  return (
    <div>
      Home
      <div>{JSON.stringify(match)}</div>
      <Button onClick={() => navigate('/mypage')}>MyPage</Button>
    </div>
  )
}
