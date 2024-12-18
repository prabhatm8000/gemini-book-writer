import React, { useEffect, useRef, useState } from 'react';

const Output = ({ selector, dispatch }) => {
    const [view, setView] = useState("book")
    const [htmlContent, setHtmlContent] = useState(null);
    const [error, setError] = useState(null)
    const [gettingHtml, setGettingHtml] = useState(false)
    const [gettingPdf, setGettingPdf] = useState(false)
    const iframeRef = useRef();

    const generatePdf = async () => {
        setView("html")
        setError(null)

        if (selector?.bookSummary === null || selector?.chapters === null) {
            setError("Please generate summary and content first")
            return
        }

        setGettingPdf(true)
        try {
            const res = await fetch("http://localhost:5000/api/generate-pdf", {
                method: "GET",
            })

            if (!res.ok) {
                setGettingPdf(false)
                setError("Something went wrong")
                return
            }

            const blob = await res.blob(); // Get the PDF as a Blob
            const url = window.URL.createObjectURL(blob); // Create a URL for the Blob
            const a = document.createElement('a'); // Create a link element
            a.href = url;

            // Use the `Content-Disposition` header to determine the filename
            const contentDisposition = res.headers.get('content-disposition');
            let fileName = 'output.pdf'; // Default filename

            if (contentDisposition && contentDisposition.includes('filename=')) {
                const filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
                const matches = filenameRegex.exec(contentDisposition);
                if (matches != null && matches[1]) {
                    fileName = matches[1].replace(/['"]/g, '');
                }
            }

            a.download = fileName;
            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url);

            setGettingPdf(false)
        } catch (error) {
            setGettingPdf(false)
            throw error
        }
    };

    const getHTML = async () => {
        setView("html")
        setError(null)

        if (selector?.bookSummary === null || selector?.chapters === null) {
            setError("Please generate summary and content first")
            return
        }

        setGettingHtml(true)
        const res = await fetch("http://localhost:5000/api/generate-html", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                bookSummary: selector?.bookSummary,
                bookContent: selector?.chapters
            })
        })

        if (!res.ok) {
            setGettingHtml(false)
        }

        const html = await res.text()
        setHtmlContent(html)
    }

    const handleJsonDownload = (e, type) => {
        let data;
        if (type === "book") {
            data = { bookSummary: selector.bookSummary, chapters: selector.chapters }
        } else if (type === "metadata") {
            data = selector.bookSummary
        }

        if (!data) {
            return
        }

        const json = JSON.stringify(data, null, 2);
        const blob = new Blob([json], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = e.target.innerText;
        link.click();
        URL.revokeObjectURL(url);
    };

    const handleHTMLBtn = () => {
        setView("html")
        getHTML()
    }

    // auto scroll to bottom
    useEffect(() => {
        const ele = document.getElementById('output')
        if (ele && view === "book") {
            ele.scrollTo(0, ele.scrollHeight);
        }
    }, [view, selector?.chapters]);

    return (
        <div className="content-container" id="output-container">
            <h3>2. Output</h3>
            <div className='btn-group'>
                <button className={`btn1 ${view === "json" ? "border-2-white" : "border-2"}`} onClick={() => setView("json")}>Raw Json</button>

                <button className={`btn1 ${view === "book" ? "border-2-white" : "border-2"}`} onClick={() => setView("book")}>Chapters</button>

                <button
                    className={`btn1 ${view === "html" ? "border-2-white" : "border-2"}`}
                    onClick={handleHTMLBtn}>
                    <span>
                        Preview
                    </span>
                    {
                        gettingHtml &&
                        <svg className="loading-circle" width="18" height="18" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="#ffffff50" strokeWidth="4"></circle>
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                    }
                </button>

                {
                    htmlContent && view === "html" &&
                    <button
                        className="btn1 flex-gap-10"
                        disabled={gettingPdf}
                        onClick={generatePdf}>
                        <span>
                            Generate PDF
                        </span>
                        {
                            (gettingPdf) &&
                            <svg className="loading-circle" width="18" height="18" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="#ffffff50" strokeWidth="4"></circle>
                                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                            </svg>
                        }
                    </button>
                }

                {view === "json" &&
                    <button
                        className="btn1"
                        disabled={gettingHtml}
                        onClick={(e) => handleJsonDownload(e, "book")}>
                        {document.title.replace(/ /g, '-')}-.json
                    </button>

                }
                {selector?.bookSummary &&
                    <button
                        className="btn1"
                        onClick={(e) => handleJsonDownload(e, "metadata")}>
                        {document.title.replace(/ /g, '-')}-metadata.json
                    </button>
                }
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
                        {selector?.bookSummary && selector?.chapters.length > 0 &&
                            <pre>
                                {JSON.stringify({ bookSummary: selector.bookSummary, chapters: selector.chapters }, null, 4)}
                            </pre>
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
                                    style={{ width: "100%", height: "98%", background: "#fff" }}
                                    srcDoc={htmlContent} // Load the HTML content directly
                                /> : ""
                        }
                    </>
                }

                {error || selector.error && <div className='error'>{error || selector.error?.message}</div>}

                {selector?.globalLoading && (
                    <p>Waiting for the output...</p>
                )}
            </div>
        </div >
    )
}

export default Output
