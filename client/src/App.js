import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';

function App() {
  const [keyword, setKeyword] = useState('');
  const [generated, setGenerated] = useState('');
  const [posts, setPosts] = useState([]);
  const [selectedPost, setSelectedPost] = useState('');
  const [postContent, setPostContent] = useState('');

  useEffect(() => {
    axios.get('/api/list_posts').then(res => setPosts(res.data));
  }, []);

  const generatePost = () => {
    axios.get(`/generate?keyword=${encodeURIComponent(keyword)}`)
      .then(res => setGenerated(res.data.blog_post))
      .catch(() => setGenerated('Error generating post.'));
  };

  const viewPost = (filename) => {
    axios.get(`/api/get_post/${filename}`)
      .then(res => setPostContent(res.data))
      .catch(() => setPostContent('Error loading post.'));
    setSelectedPost(filename);
  };

  return (
    <div style={{padding: 20}}>
      <h1>AI Blog Generator</h1>
      <div>
        <input
          value={keyword}
          onChange={e => setKeyword(e.target.value)}
          placeholder="Enter keyword"
        />
        <button onClick={generatePost}>Generate Blog Post</button>
      </div>
      {generated && (
        <div>
          <h2>Generated Blog Post</h2>
          <ReactMarkdown>{generated}</ReactMarkdown>
        </div>
      )}
      <hr />
      <h2>Previous Blog Posts</h2>
      <ul>
        {posts.map(f => (
          <li key={f}>
            <button onClick={() => viewPost(f)}>{f}</button>
          </li>
        ))}
      </ul>
      {selectedPost && (
        <div>
          <h3>{selectedPost}</h3>
          <ReactMarkdown>{postContent}</ReactMarkdown>
        </div>
      )}
    </div>
  );
}

export default App;
