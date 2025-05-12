// import { useState } from 'react'
// import axios from 'axios'

// export default function Home() {
//   const [form, setForm] = useState({ travel: 0, groceries: 0, dining: 0 })
//   const [result, setResult] = useState(null)

//   const handleSubmit = async (e) => {
//     e.preventDefault()
//     try {
//       const res = await axios.post("http://localhost:8000/recommend", form)
//       setResult(res.data.recommended_card)
//     } catch (error) {
//       console.error("Error fetching recommendation:", error)
//     }
//   }

//   return (
//     <div style={{ padding: 40 }}>
//       <h1>Card Recommender</h1>
//       <form onSubmit={handleSubmit}>
//         {["travel", "groceries", "dining"].map(cat => (
//           <div key={cat}>
//             <label>{cat}</label>
//             <input
//               type="number"
//               value={form[cat]}
//               onChange={e => setForm({ ...form, [cat]: +e.target.value })}
//               required
//             />
//           </div>
//         ))}
//         <button type="submit">Get Recommendation</button>
//       </form>
//       {result && <h3>Recommended Card: {result}</h3>}
//     </div>
//   )
// }
import { useState } from 'react'
import axios from 'axios'

export default function Home() {
  const [form, setForm] = useState({ travel: 0, groceries: 0, dining: 0 })
  const [result, setResult] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    try {
      const res = await axios.post("http://localhost:8000/recommend", form)
      setResult(res.data.recommended_card)
    } catch (error) {
      console.error("Error fetching recommendation:", error)
    }
  }

  return (
    <div style={styles.container}>
      <h1 style={styles.header}>Card Recommender</h1>
      <form onSubmit={handleSubmit} style={styles.form}>
        {["travel", "groceries", "dining"].map(cat => (
          <div key={cat} style={styles.inputContainer}>
            <label style={styles.label}>{cat}</label>
            <input
              type="number"
              value={form[cat]}
              onChange={e => setForm({ ...form, [cat]: +e.target.value })}
              required
              style={styles.input}
            />
          </div>
        ))}
        <button type="submit" style={styles.button}>Get Recommendation</button>
      </form>
      {result && <h3 style={styles.result}>Recommended Card: {result}</h3>}
    </div>
  )
}

const styles = {
  container: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    height: '100vh',
    backgroundColor: '#f4f4f9',
    fontFamily: 'Arial, sans-serif',
  },
  header: {
    fontSize: '36px',
    marginBottom: '30px',
    color: '#4A90E2',
  },
  form: {
    backgroundColor: 'white',
    padding: '20px 40px',
    borderRadius: '8px',
    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
    width: '300px',
    textAlign: 'center',
  },
  inputContainer: {
    marginBottom: '20px',
  },
  label: {
    fontSize: '16px',
    marginBottom: '5px',
    color: '#333',
    fontWeight: 'bold',
  },
  input: {
    width: '100%',
    padding: '8px',
    fontSize: '16px',
    border: '1px solid #ccc',
    borderRadius: '4px',
    boxSizing: 'border-box',
    marginTop: '5px',
  },
  button: {
    backgroundColor: '#4A90E2',
    color: 'white',
    border: 'none',
    padding: '10px 20px',
    borderRadius: '4px',
    fontSize: '16px',
    cursor: 'pointer',
    width: '100%',
  },
  result: {
    marginTop: '20px',
    fontSize: '18px',
    fontWeight: 'bold',
    color: '#28a745',
  }
}
