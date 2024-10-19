import React, { useEffect, useRef, useState } from 'react';

const Output = ({ selector, dispatch }) => {
    const [view, setView] = useState("book")
    const [htmlContent, setHtmlContent] = useState(null);
    const [error, setError] = useState(null)
    const iframeRef = useRef();

    const printPdf = () => {
        const iframe = iframeRef.current;

        // Ensure the iframe is loaded and accessible
        if (iframe) {
            iframe.contentWindow.focus();
            iframe.contentWindow.print();
        }
    };

    const handleGeneratePdfBtn = async () => {
        setView("html")
        setError(null)

        if (selector?.bookSummary === null || selector?.chapters === null) {
            setError("Please generate summary and content first")
            return
        }

        const res = await fetch("http://localhost:5000/api/generate-pdf", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                bookSummary: selector?.bookSummary,
                bookContent: selector?.chapters
            })
        })

        const html = await res.text()
        setHtmlContent(html)
    }

    const handleDownload = (data) => {
        const json = JSON.stringify(data, null, 2);
        const blob = new Blob([json], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `${document.title}-metadata.json`;
        link.click();
        URL.revokeObjectURL(url);
    };

    useEffect(() => {
        if (view === "html" && !htmlContent) {
            handleGeneratePdfBtn()
        }
    }, [htmlContent, view])

    return (
        <div className="content-container" id="output-container">
            <h3>2. Output</h3>
            <div className='btn-group'>
                <button className="btn1" onClick={() => setView("json")}>JSON</button>
                <button className="btn1" onClick={() => setView("book")}>Book</button>
                <button className="btn1" onClick={() => setView("html")}>HTML</button>
                {htmlContent && <button className="btn1" onClick={printPdf}>Generate PDF</button>}
                {selector?.bookSummary && <button className="btn1" onClick={() => handleDownload(selector.bookSummary)}>{document.title}-metadata.json</button>}
            </div>

            <div id="output" className={selector?.error ? 'error' : ''}>
                {
                    view === "book" &&
                    <>
                        {selector?.chapters?.map((chapter, index) => (
                            <div key={index} className='chapters'>
                                <h3>{`${chapter?.chapterNo}. ${chapter?.chapterName}`}</h3>
                                < div >
                                    {chapter?.chapterContent?.map((paragraph, index) => (
                                        <p className='chapter-para' key={index}>{paragraph}</p>
                                    ))}
                                </div>
                            </div>
                        ))}
                    </>
                }

                {
                    view === "json" && <>
                        {
                            "json data pending to work"
                        }
                    </>
                }

                {
                    view === "html" && <>
                        {
                            htmlContent ?
                                <iframe
                                    ref={iframeRef}
                                    title="Content IFrame"
                                    style={{ width: "100%", height: "100%", background: "#fff" }}
                                    srcDoc={htmlContent} // Load the HTML content directly
                                /> : ""
                        }
                    </>
                }

                {error && <p className='error'>{error}</p>}

                {selector?.globalLoading && (
                    <p>Waiting for the output...</p>
                )}
            </div>
        </div >
    )
}

export default Output
