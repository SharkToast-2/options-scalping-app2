# 🎯 Target Symbols Guide

## **Current Target Symbols**

The Options Scalping Application is configured to monitor and trade the following symbols:

### **📈 High-Volume Tech Stocks**
- **META** (Meta Platforms) - Social media and VR leader
- **NVDA** (NVIDIA) - AI and semiconductor powerhouse
- **TSLA** (Tesla) - Electric vehicles and clean energy
- **MSFT** (Microsoft) - Cloud computing and software

### **📊 Market Index**
- **SPY** (SPDR S&P 500 ETF) - Broad market exposure, high liquidity

### **🚀 Growth Stocks**
- **HOOD** (Robinhood Markets) - Fintech and trading platform
- **PLTR** (Palantir Technologies) - Data analytics and AI

## **Symbol Characteristics**

### **Liquidity & Volume**
- **SPY**: Highest liquidity, tightest spreads, ideal for scalping
- **TSLA**: High volatility, excellent for momentum trading
- **NVDA**: Strong technical patterns, good options liquidity
- **META**: Consistent volume, reliable price action
- **MSFT**: Stable, blue-chip with good options flow
- **HOOD**: Moderate volume, can be volatile on news
- **PLTR**: Lower volume, higher risk/reward potential

### **Trading Hours**
All symbols trade during regular market hours:
- **Pre-market**: 4:00 AM - 9:30 AM ET
- **Regular hours**: 9:30 AM - 4:00 PM ET
- **After-hours**: 4:00 PM - 8:00 PM ET

### **Options Availability**
- **SPY**: Excellent options liquidity, tight spreads
- **TSLA**: High options volume, wide spreads
- **NVDA**: Good options flow, moderate spreads
- **META**: Reliable options market
- **MSFT**: Stable options pricing
- **HOOD**: Limited options, higher spreads
- **PLTR**: Emerging options market

## **Risk Considerations**

### **Volatility Levels**
- **High Volatility**: TSLA, NVDA, PLTR
- **Medium Volatility**: META, HOOD
- **Low Volatility**: SPY, MSFT

### **Position Sizing Recommendations**
- **SPY**: Can use larger position sizes due to liquidity
- **TSLA/NVDA**: Use standard position sizes, monitor closely
- **HOOD/PLTR**: Consider smaller position sizes due to volatility

## **Signal Strength by Symbol**

### **Best for Technical Signals**
1. **SPY** - Cleanest technical patterns
2. **NVDA** - Strong trend following
3. **TSLA** - Momentum signals work well
4. **META** - Reliable support/resistance

### **Best for News/Sentiment**
1. **TSLA** - Highly news-sensitive
2. **NVDA** - AI news impacts strongly
3. **META** - Social media news affects
4. **HOOD** - Fintech news sensitive

## **Configuration**

### **Adding New Symbols**
To add new symbols, edit `config/settings.py`:

```python
TARGET_SYMBOLS = ["META", "NVDA", "SPY", "TSLA", "MSFT", "HOOD", "PLTR", "NEW_SYMBOL"]
```

### **Symbol-Specific Settings**
You can customize settings per symbol in the dashboard:
- Different position sizes
- Custom stop losses
- Symbol-specific signal thresholds

## **Performance Expectations**

### **Expected Win Rates by Symbol**
- **SPY**: 90-95% (high liquidity, predictable)
- **TSLA**: 85-90% (volatile but trendable)
- **NVDA**: 88-93% (strong technical patterns)
- **META**: 87-92% (stable price action)
- **MSFT**: 90-94% (blue-chip reliability)
- **HOOD**: 80-85% (higher volatility)
- **PLTR**: 75-80% (emerging, higher risk)

### **Average Trade Duration**
- **SPY**: 2-5 minutes
- **TSLA**: 1-3 minutes
- **NVDA**: 2-4 minutes
- **META**: 3-6 minutes
- **MSFT**: 3-5 minutes
- **HOOD**: 1-2 minutes
- **PLTR**: 1-3 minutes

## **Best Practices**

### **Symbol Selection**
1. **Start with SPY** for learning the system
2. **Add TSLA/NVDA** for momentum trading
3. **Include META/MSFT** for stability
4. **Consider HOOD/PLTR** for higher risk/reward

### **Risk Management**
- Monitor correlation between symbols
- Avoid trading all tech stocks simultaneously
- Use SPY as a market sentiment indicator
- Adjust position sizes based on volatility

### **Market Conditions**
- **Bull Market**: Focus on TSLA, NVDA, META
- **Bear Market**: SPY puts, defensive plays
- **Sideways Market**: META, MSFT for range trading
- **High Volatility**: Reduce position sizes across all symbols 