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
                    className='btn1 flex-gap-10'
                    disabled={selector?.globalLoading || loading}>
                    <span>
                        Generate Chapters
                    </span>
                    {
                        (loading || selector.globalLoading) &&
                        <svg className="loading-circle" width="18" height="18" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="#ffffff50" strokeWidth="4"></circle>
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>

                    }
                </button>
            </div>
        </div>
    )
}

export default IdeaCard
