import React from 'react'

const Output = () => {
    return (
        <div className="content-container" id="output-container">
            <h3>2. Output</h3>
            <div className='btn-group'>
                <button className="btn1">JSON</button>
                <button className="btn1">Book</button>
                <button className="btn1">Generate PDF</button>
            </div>
            <div id="output">waiting for response...</div>
        </div>
    )
}

export default Output
