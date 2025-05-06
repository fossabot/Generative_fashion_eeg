import { useEffect, useState } from 'react'
import BasicTable from './components/datatable';

function Dashboard() {

    return (
        <div style={{
            fontFamily: 'Avenir', fontWeight: 'bold', padding: '2rem',
        }}>
            <h1>Dataoverview</h1>
            <BasicTable></BasicTable>
        </div>

    )
}

export default Dashboard;
