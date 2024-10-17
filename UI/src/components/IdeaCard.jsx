import React from 'react'

const IdeaCard = ({ idea, handleGenerateChaptersBtn, index, selector, loading }) => {
    return (
        <div key={index} className='idea-card'>
            <span>{index + 1}.</span>
            <div>
                <h3>{idea?.title}</h3>
                <div>
                    <strong>
                        Style
                    </strong>
                    <span className='light-text'>
                        {idea?.style}
                    </span>
                </div>

                <div>
                    <strong>Genre </strong>
                    <span className='light-text'>
                        {idea?.genre?.join(', ')}
                    </span>
                </div>
                <div>
                    <strong>
                        Description
                    </strong>
                    <span className='light-text'>
                        {idea?.description}
                    </span>
                </div>

                <button
                    onClick={() => handleGenerateChaptersBtn(index)}
                    className='btn1'
                    disabled={selector?.globalLoading || loading}>
                    Generate Chapters
                </button>
            </div>
        </div>
    )
}

export default IdeaCard
