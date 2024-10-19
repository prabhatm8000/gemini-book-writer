import React from 'react'

const BookSummary = ({ bookSummary, handleGenerateFullBook }) => {
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

            <button className='btn1 generate-book-btn' onClick={handleGenerateFullBook}>Generate Full Book</button>
        </>
    )
}

export default BookSummary
