import React, { useState, useEffect } from 'react';
import { Table } from 'antd';
import axios from 'axios';

const FileUpload = ({ onFileProcessed, data: propsData, columns: propsColumns, readOnly = false }) => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(propsData || []);
  const [columns, setColumns] = useState([]);

  useEffect(() => {
    if (propsData) {
      setData(propsData);
    }
    if (propsColumns) {
      const formattedColumns = propsColumns.map(col => ({
        title: col,
        dataIndex: col,
        key: col,
      }));
      setColumns(formattedColumns);
    }
  }, [propsData, propsColumns]);

  const handleFileChange = async (event) => {
    const selectedFile = event.target.files[0];
    if (!selectedFile) return;

    setFile(selectedFile);
    setLoading(true);

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await axios.post('http://localhost:8000/api/files/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      const { data: tableData, columns: tableColumns } = response.data;
      
      // Format columns for Ant Design Table
      const formattedColumns = tableColumns.map(col => ({
        title: col,
        dataIndex: col,
        key: col,
      }));

      setData(tableData);
      setColumns(formattedColumns);
      onFileProcessed(response.data);
    } catch (error) {
      console.error('Error uploading file:', error);
      alert('Error uploading file. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="file-upload">
      {!readOnly && (
        <input
          type="file"
          accept=".csv,.xlsx"
          onChange={handleFileChange}
          disabled={loading}
        />
      )}
      {loading && <p>Loading...</p>}
      {data.length > 0 && (
        <Table
          dataSource={data}
          columns={columns}
          scroll={{ x: true }}
          pagination={{ pageSize: 10 }}
        />
      )}
    </div>
  );
};

export default FileUpload; 