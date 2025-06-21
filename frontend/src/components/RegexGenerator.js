import React, { useState } from 'react';
import { Input, Button, Select, message } from 'antd';
import axios from 'axios';

const { TextArea } = Input;

const RegexGenerator = ({ fileId, columns, onRegexGenerated }) => {
  const [description, setDescription] = useState('');
  const [replacement, setReplacement] = useState('');
  const [selectedColumn, setSelectedColumn] = useState('');
  const [loading, setLoading] = useState(false);
  const [regex, setRegex] = useState('');

  const handleGenerateRegex = async () => {
    if (!description) {
      message.error('Please enter a description');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(`http://localhost:8000/api/files/${fileId}/generate_regex/`, {
        description
      });
      setRegex(response.data.regex);
      onRegexGenerated(response.data.regex);
    } catch (error) {
      console.error('Error generating regex:', error);
      message.error('Error generating regex. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleReplace = async () => {
    if (!regex || !replacement || !selectedColumn) {
      message.error('Please fill in all fields');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(`http://localhost:8000/api/files/${fileId}/replace_text/`, {
        regex,
        replacement,
        column: selectedColumn
      });
      onRegexGenerated(regex, response.data);
    } catch (error) {
      console.error('Error replacing text:', error);
      message.error('Error replacing text. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="regex-generator">
      <div className="input-group">
        <TextArea
          placeholder="Enter natural language description (e.g., 'Find email addresses')"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          rows={4}
        />
        <Button
          type="primary"
          onClick={handleGenerateRegex}
          loading={loading}
          style={{ marginTop: '10px' }}
        >
          Generate Regex
        </Button>
      </div>

      {regex && (
        <div className="regex-section">
          <p>Generated Regex: <code>{regex}</code></p>
          <div className="replacement-section">
            <Input
              placeholder="Enter replacement text"
              value={replacement}
              onChange={(e) => setReplacement(e.target.value)}
              style={{ marginBottom: '10px' }}
            />
            <Select
              placeholder="Select column"
              value={selectedColumn}
              onChange={setSelectedColumn}
              style={{ width: '100%', marginBottom: '10px' }}
            >
              {columns.map(col => (
                <Select.Option key={col} value={col}>
                  {col}
                </Select.Option>
              ))}
            </Select>
            <Button
              type="primary"
              onClick={handleReplace}
              loading={loading}
            >
              Apply Replacement
            </Button>
          </div>
        </div>
      )}
    </div>
  );
};

export default RegexGenerator; 