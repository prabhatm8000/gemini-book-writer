import React from 'react'

const BookSummary = ({ bookSummary, handleGenerateFullBook, loading }) => {
    return (
        <>
            <h2>{bookSummary?.title}</h2>

            <div>
                <strong>No. of Chapters</strong> <span>{bookSummary?.totalChapters}</span>
            </div>

            <div>
                <strong>Genre </strong>
                <span className='light-text'>
                    {bookSummary?.genre?.join(', ')}
                </span>
            </div>

            <div className='summary'>
                <h3>
                    Summary
                </h3>
                <span className='light-text'>
                    {bookSummary?.summary}
                </span>
            </div>

            <div className='chapters'>
                {bookSummary?.chapters?.map((chapter, index) => (
                    <div key={index}>
                        <strong>
                            {`${chapter?.chapterNo}. ${chapter?.chapterName}`}
                        </strong>: <span className='light-text'>
                            {chapter?.chapterSummary}
                        </span>
                    </div>
                ))}
            </div>

            <button className='btn1 generate-book-btn flex-gap-10' onClick={handleGenerateFullBook}>
                Generate Full Book
                {
                    (loading) &&
                    <svg className="loading-circle" width="18" height="18" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="#ffffff50" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                }
            </button>
        </>
    )
}

export default BookSummary
