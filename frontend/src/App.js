import React, { useState } from 'react';
import { Layout, Typography, Card } from 'antd';
import FileUpload from './components/FileUpload';
import RegexGenerator from './components/RegexGenerator';
import './App.css';

const { Header, Content } = Layout;
const { Title } = Typography;

function App() {
  const [fileData, setFileData] = useState(null);
  const [processedData, setProcessedData] = useState(null);

  const handleFileProcessed = (data) => {
    setFileData(data);
    setProcessedData(null);
  };

  const handleRegexGenerated = (regex, newData) => {
    if (newData) {
      setProcessedData(newData);
    }
  };

  return (
    <Layout className="layout">
      <Header>
        <Title level={3} style={{ color: 'white', margin: 0 }}>
          Text Pattern Matcher
        </Title>
      </Header>
      <Content style={{ padding: '24px', minHeight: 'calc(100vh - 64px)' }}>
        <Card title="Upload File" style={{ marginBottom: '24px' }}>
          <FileUpload onFileProcessed={handleFileProcessed} />
        </Card>

        {fileData && (
          <Card title="Generate Regex and Replace Text">
            <RegexGenerator
              fileId={fileData.id}
              columns={fileData.columns}
              onRegexGenerated={handleRegexGenerated}
            />
          </Card>
        )}

        {processedData && (
          <Card title="Processed Data" style={{ marginTop: '24px' }}>
            <FileUpload
              data={processedData.data}
              columns={processedData.columns}
              readOnly
            />
          </Card>
        )}
      </Content>
    </Layout>
  );
}

export default App;
