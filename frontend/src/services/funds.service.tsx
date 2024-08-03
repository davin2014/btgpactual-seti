import { Fund } from "../models/fund.model";
import { API_BASE_URL } from "../config/config";

export const fetchFunds = async (): Promise<Fund[]> => {
    try {
      const response = await fetch(`${API_BASE_URL}funds/`);
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error fetching funds:', error);
      throw error;
    }
  };


  export const fetchFundNames = async (fundIds: string[]): Promise<{ [key: string]: string }> => {
    try {
      const fundNamesResponse = await Promise.all(
        fundIds.map(async (fundId) => {
          const response = await fetch(`${API_BASE_URL}funds/${fundId}`);
          if (!response.ok) {
            throw new Error(`Network response was not ok for fundId: ${fundId}`);
          }
          const data = await response.json();
          return { fundId, name: data.name };
        })
      );
  
      const fundNamesMap = fundNamesResponse.reduce((acc, { fundId, name }) => {
        acc[fundId] = name;
        return acc;
      }, {} as { [key: string]: string });
  
      return fundNamesMap;
    } catch (error) {
      console.error('Error fetching fund names:', error);
      throw error;
    }
  };



